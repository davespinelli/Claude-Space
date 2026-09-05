#!/usr/bin/env python3
"""QUEUE idea 173 — is-the-ladder-endpoint-a-general-selector-artefact  (cloud, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 173)
    "idea 171 found the SLEEVE 'win' is entirely a monotone truncated ladder: the IS-Sharpe
     argmax equals the OOS oracle in 53/53 books at f=0.30, and RANDOM also beats the constant
     there.  Audit every ladder the project has ever fitted for the same signature (Spearman of
     mean OOS score vs ladder rank, and share of books whose argmax sits at an endpoint), and
     report how many published 'the argmax is X' claims are really 'X is the edge of the grid
     I chose'.  Max 2 params."

WHAT "THE LADDER-ENDPOINT SIGNATURE" MEANS, MADE FALSIFIABLE
    A dial fitted by IS-argmax on a ladder produces a "win" for one of two reasons:
      (E) ENDPOINT ARTEFACT — the OOS score is MONOTONE in the dial over the grid the project
          chose, so the OOS oracle sits at a grid edge by construction and ANY selector that
          drifts toward that edge (IS-argmax, but also a RANDOM pick, which is pulled toward
          the better half of a monotone ladder) beats the interior incumbent.  The "argmax is
          X" claim then reports where the grid was truncated, not where the optimum is.
      (S) GENUINE SKILL — the OOS oracle is INTERIOR, and the IS window still finds it more
          often than chance and captures more of the oracle's edge than a RANDOM pick.
    Three measurements separate them, exactly the ones idea 173 names:
      m1  share of ladder instances whose OOS argmax (the oracle) sits at an ENDPOINT,
          against the chance null 2/K, and the same for the IS argmax;
      m2  Spearman(ladder rank, OOS score) — within each instance and against the across-book
          MEAN OOS score, which is idea 171's stated diagnostic;
      m3  CAPTURE — the fraction of (oracle - constant) that the IS pick earns, against the
          fraction a RANDOM pick earns.  Under (E) RANDOM's capture is large and positive;
          under (S) it is near zero while the IS pick's is not.

CORPUS — 90 ladder instances, every point reported
    3 panels    u56 (research/universe.json ETF+mega-cap), broad (universe_broad.json, 136
                large caps), small (data/prices_small.csv, sub-$2B, tickers with
                max_1d_move >= 1.0 in data/small_meta.csv DROPPED first)
    3 signals   COMP  RULES v1's composite (mean pct-rank of 12-1 mom, 6m, 3m)
                MOM   raw 12-1 momentum
                R6    raw 6-month return
    2 cost rungs 10 bps (PROTOCOL) and 25 bps, derived EXACTLY from the zero-cost run and the
                engine's own turnover series (port_c = port_0 - turnover * c / 1e4), so the
                cost axis costs no extra engine runs and introduces no new convention.
    = 18 book-cells.  Each book-cell is laddered on FIVE dials, one at a time, everything else
    held at the anchor (n=20, g=0.75, freq=W, max_vol=0.60, p=0.5):
        GROSS    g       0.45 0.60 0.75 0.90 1.05 1.20 1.35      (7)
        COUNT    n       5 10 20 40 80                           (5)
        CADENCE  freq    D W M Q                                 (4)
        VOLCAP   max_vol 0.30 0.45 0.60 0.80 none                (5)
        VOLPOW   p       0.00 0.25 0.50 0.75 1.00                (5)   s /= vol20**p
    18 x 5 = 90 ladder instances, 18 x 26 = 468 ladder-point rows, ALL written to .grid.csv.

TUNED PARAMETERS — one per row, never two
    Each row varies EXACTLY ONE dial from the anchor; the anchor itself is fixed in advance
    (n=20 / g=0.75 is the 2026-09-04 4b KEEP's construction, freq=W and max_vol=0.60 are
    RULES v1's, p=0.5 is RULES v1's vol scaler).  Panels, signals, cost rungs and the OOS
    window are reported axes, never selected on.  The second "parameter" in the QUEUE's budget
    is the SELECTOR (IS-argmax / RANDOM / ORACLE / CONSTANT), and all four are reported for
    every instance.

BOOK CONSTRUCTION — one convention only (idea 127's "literal")
    w = (rank <= n) * g / n on names passing RULES v1's hard eligibility gate
    (px > 200d MA) & (vol20 < max_vol); unfilled slots are cash.  No renormalisation, no
    sleeve, no overlay.  Weights decided at close t, applied at t+1 by the engine (PROTOCOL 2).

WALK-FORWARD (PROTOCOL rule 8) — this run IS a walk-forward experiment
    IS window  = sample start .. 2016-12-31, read by the selector.
    OOS window = 2017-01-01 .. end, read ONCE per instance.
    For every one of the 90 instances the IS pick's OOS CAGR / Sharpe / MaxDD is reported
    against (a) the anchor point, (b) RULES v1 on the same panel at the same cost rung, and
    (c) SPY, and BOTH KEEP paths are evaluated on the full sample and again on the OOS window:
      4a  Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1.
      4b  Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  At least one dial shows idea 171's signature outright: OOS-oracle endpoint share >= 0.80
        against the 2/K null, with |Spearman(rank, mean OOS Sharpe)| >= 0.9.
    P2  GROSS is that dial.  Its OOS Sharpe should be near-flat and weakly monotone (idea 174
        found Sharpe moves 0.973-0.978 over a whole gross range), so its argmax is decided by
        noise at the edge.
    P3  CADENCE is NOT that dial — idea 175 reports its oracle interior in 96.2% of books — so
        its endpoint share should be at or below the null.  If CADENCE also comes out at the
        endpoint here, idea 175's single surviving dial is in trouble.
    P4  RANDOM's capture is positive on every dial whose oracle-endpoint share is above the
        null, and near zero on the rest.  This is the operational form of the artefact.
    P5  Fewer than 10 of the 90 instances produce a rule-8 OOS pick that clears 4b on the OOS
        window; the audit is about selection, not about promoting a book.

CAVEATS carried, not buried
    * SURVIVORSHIP.  All three panels are CURRENT constituents (idea 54).  The small panel is
      the sub-$2B screen as it stands today with delisted/acquired names absent entirely; that
      bias is one-directional and falls hardest on the beaten-down cohort the trend gate
      excludes, so every CAGR here is optimistic and no level in this file is an achievable
      return.  The small panel additionally drops the 44 tickers with max_1d_move >= 1.0.
    * WINDOW COMPOSITION (idea 111).  The IS window holds fewer SPY-drawdown years than the OOS
      window, and the small panel's IS window is only 2011-2016.  A selector reading IS is
      reading a calmer regime; this inflates every "IS says X" statement equally, and the
      RANDOM and CONSTANT controls are the defence against reading that as skill.
    * This run audits the FIVE dials it re-runs.  The textual census at the end counts published
      "argmax" claims and which dial each concerns; it does NOT re-verify claims about dials
      outside this grid (sleeve fraction, breadth gates, entry budgets).
    * Every row is t+1 execution at 10 or 25 bps only.

Deterministic (seed 173), standalone, no network.
Writes .grid.csv (468 points), .instances.csv (90), .walkforward.csv (90), .census.csv,
.result.md and .console.txt.
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
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_is-the-ladder-endpoint-a-general-selector-artefact_cloud"
OUT = ROOT / "research" / "backtests"
SEED = 173
IS_END = pd.Timestamp("2016-12-31")

ANCHOR = dict(n=20, g=0.75, freq="W", max_vol=0.60, p=0.5)
LADDERS = {
    "GROSS":   ("g",       [0.45, 0.60, 0.75, 0.90, 1.05, 1.20, 1.35]),
    "COUNT":   ("n",       [5, 10, 20, 40, 80]),
    "CADENCE": ("freq",    ["D", "W", "M", "Q"]),
    "VOLCAP":  ("max_vol", [0.30, 0.45, 0.60, 0.80, 99.0]),
    "VOLPOW":  ("p",       [0.00, 0.25, 0.50, 0.75, 1.00]),
}
SIGNALS = ["COMP", "MOM", "R6"]
COSTS = [10.0, 25.0]

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


def load_panels():
    return {"u56": load_universe(), "broad": load_universe(broad=True), "small": small_panel()}


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


def weights(px, sig, n, g, max_vol, p):
    """Literal top-n equal weight at gross g among eligible names; cash for empty slots."""
    s = raw_signal(px, sig)
    above, vol20 = gates(px)
    if p:
        s = s / vol20.clip(lower=0.08) ** p
    elig = s.where(above & (vol20 < max_vol))
    rank = elig.rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (g / n)


# ----------------------------------------------------------------------------- metrics
def spearman(a, b):
    """Rank correlation without scipy (the sandbox has none): Pearson on ranks."""
    ra, rb = pd.Series(a).rank(), pd.Series(b).rank()
    if ra.std(ddof=0) == 0 or rb.std(ddof=0) == 0:
        return np.nan
    return float(np.corrcoef(ra.values, rb.values)[0, 1])


def win(r, lo=None, hi=None):
    if lo is not None:
        r = r.loc[lo:]
    if hi is not None:
        r = r.loc[:hi]
    return r


def stats(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def full_row(r):
    """CAGR/Sharpe/MaxDD on full, H1, H2, IS, OOS."""
    h = len(r) // 2
    out = {}
    for tag, x in (("F", r), ("H1", r.iloc[:h]), ("H2", r.iloc[h:]),
                   ("IS", win(r, hi=IS_END)), ("OOS", win(r, lo=IS_END + pd.Timedelta(days=1)))):
        c, s, d = stats(x)
        out[f"CAGR_{tag}"], out[f"Sharpe_{tag}"], out[f"MaxDD_{tag}"] = c, s, d
    return out


def pass4a(row, base):
    return bool(row["Sharpe_H1"] > base["Sharpe_H1"] and row["Sharpe_H2"] > base["Sharpe_H2"]
                and row["MaxDD_F"] >= base["MaxDD_F"])


def pass4b(row, spy):
    return bool(row["Sharpe_H1"] > spy["Sharpe_H1"] and row["Sharpe_H2"] > spy["Sharpe_H2"]
                and row["Sharpe_OOS"] > spy["Sharpe_OOS"]
                and row["MaxDD_F"] >= 0.60 * spy["MaxDD_F"]
                and row["CAGR_F"] >= 0.70 * spy["CAGR_F"])


def pass4b_oos_window(row, spy):
    """4b read on the OOS window alone: its two halves, its Sharpe, its DD cap and CAGR floor."""
    return bool(row["oosH1"] > spy["oosH1"] and row["oosH2"] > spy["oosH2"]
                and row["Sharpe_OOS"] > spy["Sharpe_OOS"]
                and row["MaxDD_OOS"] >= 0.60 * spy["MaxDD_OOS"]
                and row["CAGR_OOS"] >= 0.70 * spy["CAGR_OOS"])


def oos_halves(r):
    o = win(r, lo=IS_END + pd.Timedelta(days=1))
    h = len(o) // 2
    return metrics(o.iloc[:h])["Sharpe"], metrics(o.iloc[h:])["Sharpe"]


# ----------------------------------------------------------------------------- run
def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    panels = load_panels()

    # ---- reference returns per panel: SPY and RULES v1 at both cost rungs
    ref = {}
    for pn, px in panels.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        b0 = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq="W")
        bret, btrn = b0["returns"].loc[start:], b0["turnover"].loc[start:]
        ref[pn] = dict(start=start, spy=spy, b_ret=bret, b_trn=btrn)
        say(f"panel {pn}: {px.shape[1]} cols, sample {start.date()}..{px.index[-1].date()}, "
            f"IS rows {len(win(spy, hi=IS_END))}, OOS rows {len(win(spy, lo=IS_END))}")

    # ---- the 468 ladder points
    grid = []
    n_runs = 0
    for pn, px in panels.items():
        start = ref[pn]["start"]
        for sig in SIGNALS:
            for lad, (dial, vals) in LADDERS.items():
                for k, v in enumerate(vals):
                    cfg = dict(ANCHOR)
                    cfg[dial] = v
                    w = weights(px, sig, cfg["n"], cfg["g"], cfg["max_vol"], cfg["p"])
                    res = backtest(px, w, cost_bps=0.0, freq=cfg["freq"])
                    r0, trn = res["returns"].loc[start:], res["turnover"].loc[start:]
                    n_runs += 1
                    for c in COSTS:
                        r = r0 - trn * c / 1e4
                        row = dict(panel=pn, signal=sig, cost=c, ladder=lad, dial=dial,
                                   value=str(v), rank=k + 1, K=len(vals),
                                   is_anchor=int(v == ANCHOR[dial]),
                                   turnover_yr=float(trn.sum() / (len(trn) / 252)))
                        row.update(full_row(r))
                        row["oosH1"], row["oosH2"] = oos_halves(r)
                        grid.append(row)
    G = pd.DataFrame(grid)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say(f"\ngrid: {n_runs} engine runs -> {len(G)} ladder-point rows "
        f"({time.time() - t0:.0f}s) -> {STEM}.grid.csv")

    # ---- reference rows (RULES v1, SPY) per panel x cost
    refrow = {}
    for pn in panels:
        spy = ref[pn]["spy"]
        srow = full_row(spy)
        srow["oosH1"], srow["oosH2"] = oos_halves(spy)
        for c in COSTS:
            b = ref[pn]["b_ret"] - ref[pn]["b_trn"] * c / 1e4
            brow = full_row(b)
            brow["oosH1"], brow["oosH2"] = oos_halves(b)
            refrow[(pn, c)] = (brow, srow)

    say("\n=== reference books (Sharpe F / H1 / H2 / OOS, CAGR_F, MaxDD_F) ===")
    for (pn, c), (brow, srow) in refrow.items():
        say(f"  {pn:5s} @{int(c)}bps  RULES v1 {brow['Sharpe_F']:.3f} / {brow['Sharpe_H1']:.3f} / "
            f"{brow['Sharpe_H2']:.3f} / {brow['Sharpe_OOS']:.3f}  "
            f"CAGR {brow['CAGR_F']:.2%}  DD {brow['MaxDD_F']:.2%}")
    for pn in panels:
        srow = refrow[(pn, COSTS[0])][1]
        say(f"  {pn:5s} SPY        {srow['Sharpe_F']:.3f} / {srow['Sharpe_H1']:.3f} / "
            f"{srow['Sharpe_H2']:.3f} / {srow['Sharpe_OOS']:.3f}  "
            f"CAGR {srow['CAGR_F']:.2%}  DD {srow['MaxDD_F']:.2%}")

    # ---- 90 ladder instances
    inst, wf = [], []
    for (pn, sig, c, lad), sub in G.groupby(["panel", "signal", "cost", "ladder"], sort=False):
        sub = sub.sort_values("rank").reset_index(drop=True)
        K = int(sub["K"].iloc[0])
        is_s = sub["Sharpe_IS"].values
        oos_s = sub["Sharpe_OOS"].values
        i_is = int(np.argmax(is_s))
        i_or = int(np.argmax(oos_s))
        i_an = int(sub.index[sub["is_anchor"] == 1][0])
        end = lambda i: int(i == 0 or i == K - 1)
        rho = spearman(np.arange(K), oos_s)
        rho_is = spearman(np.arange(K), is_s)
        rnd_draw = int(rng.integers(K))
        d_is = oos_s[i_is] - oos_s[i_an]
        d_or = oos_s[i_or] - oos_s[i_an]
        d_rand_e = float(np.mean(oos_s)) - oos_s[i_an]
        d_rand_d = oos_s[rnd_draw] - oos_s[i_an]
        cap_is = d_is / d_or if d_or > 1e-12 else np.nan
        cap_rand = d_rand_e / d_or if d_or > 1e-12 else np.nan
        inst.append(dict(
            panel=pn, signal=sig, cost=c, ladder=lad, K=K,
            anchor=sub["value"].iloc[i_an], IS_pick=sub["value"].iloc[i_is],
            oracle=sub["value"].iloc[i_or], rand_draw=sub["value"].iloc[rnd_draw],
            i_is=i_is + 1, i_oracle=i_or + 1, i_anchor=i_an + 1,
            IS_endpoint=end(i_is), oracle_endpoint=end(i_or), agree=int(i_is == i_or),
            rho_rank_OOS=rho, rho_rank_IS=rho_is,
            OOS_Sharpe_anchor=oos_s[i_an], OOS_Sharpe_ISpick=oos_s[i_is],
            OOS_Sharpe_oracle=oos_s[i_or], OOS_Sharpe_randE=float(np.mean(oos_s)),
            OOS_Sharpe_randD=oos_s[rnd_draw],
            d_IS=d_is, d_randE=d_rand_e, d_randD=d_rand_d, d_oracle=d_or,
            capture_IS=cap_is, capture_rand=cap_rand,
            OOS_range=float(oos_s.max() - oos_s.min())))

        # ---- rule 8: the IS pick read once on OOS, both KEEP paths
        pick = sub.iloc[i_is]
        anch = sub.iloc[i_an]
        brow, srow = refrow[(pn, c)]
        wf.append(dict(
            panel=pn, signal=sig, cost=c, ladder=lad, IS_pick=pick["value"],
            anchor=anch["value"], oracle=sub["value"].iloc[i_or],
            F_CAGR=pick["CAGR_F"], F_Sharpe=pick["Sharpe_F"], F_MaxDD=pick["MaxDD_F"],
            F_H1=pick["Sharpe_H1"], F_H2=pick["Sharpe_H2"], turnover_yr=pick["turnover_yr"],
            OOS_CAGR=pick["CAGR_OOS"], OOS_Sharpe=pick["Sharpe_OOS"], OOS_MaxDD=pick["MaxDD_OOS"],
            anch_OOS_CAGR=anch["CAGR_OOS"], anch_OOS_Sharpe=anch["Sharpe_OOS"],
            anch_OOS_MaxDD=anch["MaxDD_OOS"],
            base_OOS_CAGR=brow["CAGR_OOS"], base_OOS_Sharpe=brow["Sharpe_OOS"],
            base_OOS_MaxDD=brow["MaxDD_OOS"],
            spy_OOS_CAGR=srow["CAGR_OOS"], spy_OOS_Sharpe=srow["Sharpe_OOS"],
            spy_OOS_MaxDD=srow["MaxDD_OOS"],
            pass4a_full=int(pass4a(pick, brow)), pass4b_full=int(pass4b(pick, srow)),
            pass4b_oos=int(pass4b_oos_window(pick, srow)),
            anch_pass4a_full=int(pass4a(anch, brow)), anch_pass4b_full=int(pass4b(anch, srow)),
            anch_pass4b_oos=int(pass4b_oos_window(anch, srow))))

    I = pd.DataFrame(inst)
    W = pd.DataFrame(wf)
    I.to_csv(OUT / f"{STEM}.instances.csv", index=False)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    # ---- m1/m2/m3 per ladder
    say("\n=== m1  ENDPOINT SHARE (18 book-cells per ladder; null = 2/K) ===")
    say(f"{'ladder':9s} {'K':>2s} {'null':>5s} {'oracle@end':>11s} {'IS@end':>7s} "
        f"{'agree':>6s} {'null_ag':>7s}")
    per = {}
    for lad, sub in I.groupby("ladder", sort=False):
        K = int(sub["K"].iloc[0])
        per[lad] = dict(K=K, null=2 / K, oe=sub["oracle_endpoint"].mean(),
                        ie=sub["IS_endpoint"].mean(), ag=sub["agree"].mean(), nag=1 / K)
        p = per[lad]
        say(f"{lad:9s} {K:2d} {p['null']:5.3f} {p['oe']:11.3f} {p['ie']:7.3f} "
            f"{p['ag']:6.3f} {p['nag']:7.3f}")

    say("\n=== m2  MONOTONICITY  Spearman(ladder rank, OOS Sharpe) ===")
    say(f"{'ladder':9s} {'mean rho':>9s} {'|rho|>=0.9':>11s} {'rho(rank, MEAN OOS)':>20s} "
        f"{'mean OOS range':>15s}")
    for lad, sub in I.groupby("ladder", sort=False):
        K = per[lad]["K"]
        pts = G[G["ladder"] == lad].groupby("rank")["Sharpe_OOS"].mean().sort_index()
        rho_mean = spearman(np.arange(K), pts.values)
        per[lad]["rho_mean"] = rho_mean
        per[lad]["rho_within"] = sub["rho_rank_OOS"].mean()
        say(f"{lad:9s} {sub['rho_rank_OOS'].mean():9.3f} "
            f"{(sub['rho_rank_OOS'].abs() >= 0.9).mean():11.3f} {rho_mean:20.3f} "
            f"{sub['OOS_range'].mean():15.3f}")
        say("           mean OOS Sharpe by rank: " +
            "  ".join(f"{v}={x:.3f}" for v, x in
                      zip(LADDERS[lad][1], pts.values)))

    say("\n=== m3  CAPTURE of the oracle, vs a RANDOM pick (paired over 18 cells) ===")
    say(f"{'ladder':9s} {'dIS':>7s} {'t(dIS)':>7s} {'dRAND_E':>8s} {'t':>6s} {'dORACLE':>8s} "
        f"{'cap_IS':>7s} {'cap_RND':>7s} {'IS>RND':>7s}")
    for lad, sub in I.groupby("ladder", sort=False):
        def tstat(x):
            x = x.dropna().values
            return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))) if len(x) > 1 and x.std(ddof=1) > 0 else np.nan
        per[lad].update(dIS=sub["d_IS"].mean(), dRND=sub["d_randE"].mean(),
                        dORC=sub["d_oracle"].mean(),
                        capIS=sub["capture_IS"].median(), capRND=sub["capture_rand"].median())
        say(f"{lad:9s} {sub['d_IS'].mean():7.4f} {tstat(sub['d_IS']):7.2f} "
            f"{sub['d_randE'].mean():8.4f} {tstat(sub['d_randE']):6.2f} "
            f"{sub['d_oracle'].mean():8.4f} {sub['capture_IS'].median():7.3f} "
            f"{sub['capture_rand'].median():7.3f} "
            f"{(sub['d_IS'] > sub['d_randE']).mean():7.3f}")

    # ---- m4: is the artefact the LADDER, or WHERE THE CONSTANT SITS ON IT?
    # Idea 171's "RANDOM also beats the constant" was measured with the constant at f=0, the
    # LOW endpoint.  This run's anchor is interior in all five ladders by construction.  The
    # same 468 points answer both readings: re-price RANDOM against three reference constants.
    say("\n=== m4  RANDOM vs the constant, by WHERE THE CONSTANT SITS (same 468 points) ===")
    say(f"{'ladder':9s} {'anchor@':>7s} | {'d_rand vs anchor':>16s} {'win':>5s} | "
        f"{'vs LOW end':>10s} {'win':>5s} | {'vs HIGH end':>11s} {'win':>5s}")
    m4 = []
    for (pn, sig, c, lad), sub in G.groupby(["panel", "signal", "cost", "ladder"], sort=False):
        sub = sub.sort_values("rank").reset_index(drop=True)
        o = sub["Sharpe_OOS"].values
        i_an = int(sub.index[sub["is_anchor"] == 1][0])
        mean_o = float(np.mean(o))
        m4.append(dict(ladder=lad, panel=pn, signal=sig, cost=c, i_anchor=i_an + 1, K=len(o),
                       d_anchor=mean_o - o[i_an], d_low=mean_o - o[0], d_high=mean_o - o[-1]))
    M4 = pd.DataFrame(m4)
    for lad, sub in M4.groupby("ladder", sort=False):
        say(f"{lad:9s} {int(sub['i_anchor'].iloc[0]):2d}/{int(sub['K'].iloc[0]):<2d}  | "
            f"{sub['d_anchor'].mean():16.4f} {(sub['d_anchor'] > 0).mean():5.2f} | "
            f"{sub['d_low'].mean():10.4f} {(sub['d_low'] > 0).mean():5.2f} | "
            f"{sub['d_high'].mean():11.4f} {(sub['d_high'] > 0).mean():5.2f}")
    M4.to_csv(OUT / f"{STEM}.anchorposition.csv", index=False)
    say(f"  ALL ladders pooled (90): RANDOM beats an INTERIOR constant in "
        f"{(M4['d_anchor'] > 0).mean():.2f} of instances, a LOW-end constant in "
        f"{(M4['d_low'] > 0).mean():.2f}, a HIGH-end constant in {(M4['d_high'] > 0).mean():.2f}")

    say("\n=== does IS selection change anything?  share of instances with IS pick == anchor ===")
    for lad, sub in I.groupby("ladder", sort=False):
        say(f"  {lad:9s} IS pick == anchor in {int((sub['i_is'] == sub['i_anchor']).sum()):2d}/18, "
            f"oracle == anchor in {int((sub['i_oracle'] == sub['i_anchor']).sum()):2d}/18")

    say("\n=== per-panel endpoint share of the ORACLE (robustness of m1) ===")
    say(pd.crosstab(I["ladder"], I["panel"], values=I["oracle_endpoint"],
                    aggfunc="mean").to_string(float_format=lambda x: f"{x:.3f}"))
    say("\n=== per-cost endpoint share of the ORACLE ===")
    say(pd.crosstab(I["ladder"], I["cost"], values=I["oracle_endpoint"],
                    aggfunc="mean").to_string(float_format=lambda x: f"{x:.3f}"))

    say("\n=== which END?  (1 = low end of the dial, K = high end) ===")
    for lad, sub in I.groupby("ladder", sort=False):
        K = per[lad]["K"]
        lo = (sub["i_oracle"] == 1).sum()
        hi = (sub["i_oracle"] == K).sum()
        say(f"{lad:9s} oracle at low end {lo:2d}/18, high end {hi:2d}/18, interior "
            f"{18 - lo - hi:2d}/18   |  IS pick low {int((sub['i_is'] == 1).sum()):2d}, "
            f"high {int((sub['i_is'] == K).sum()):2d}")

    # ---- rule 8 / KEEP paths
    say("\n=== PROTOCOL rule 8: the IS pick read ONCE on 2017-2026 (90 instances) ===")
    say(f"  mean OOS Sharpe  IS pick {W['OOS_Sharpe'].mean():.4f}   anchor "
        f"{W['anch_OOS_Sharpe'].mean():.4f}   RULES v1 {W['base_OOS_Sharpe'].mean():.4f}   "
        f"SPY {W['spy_OOS_Sharpe'].mean():.4f}")
    say(f"  mean OOS CAGR    IS pick {W['OOS_CAGR'].mean():.2%}   anchor "
        f"{W['anch_OOS_CAGR'].mean():.2%}   RULES v1 {W['base_OOS_CAGR'].mean():.2%}   "
        f"SPY {W['spy_OOS_CAGR'].mean():.2%}")
    say(f"  mean OOS MaxDD   IS pick {W['OOS_MaxDD'].mean():.2%}   anchor "
        f"{W['anch_OOS_MaxDD'].mean():.2%}   RULES v1 {W['base_OOS_MaxDD'].mean():.2%}   "
        f"SPY {W['spy_OOS_MaxDD'].mean():.2%}")
    say(f"  IS pick beats SPY OOS Sharpe in {int((W['OOS_Sharpe'] > W['spy_OOS_Sharpe']).sum())}/90; "
        f"anchor {int((W['anch_OOS_Sharpe'] > W['spy_OOS_Sharpe']).sum())}/90")
    say(f"  KEEP paths  4a(full) IS pick {int(W['pass4a_full'].sum())}/90, anchor "
        f"{int(W['anch_pass4a_full'].sum())}/90   |   4b(full) IS pick "
        f"{int(W['pass4b_full'].sum())}/90, anchor {int(W['anch_pass4b_full'].sum())}/90   |   "
        f"4b(OOS window) IS pick {int(W['pass4b_oos'].sum())}/90, anchor "
        f"{int(W['anch_pass4b_oos'].sum())}/90")
    k4b = W[W["pass4b_full"] == 1]
    if len(k4b):
        say("\n  --- instances clearing 4b on the FULL sample ---")
        say(k4b[["panel", "signal", "cost", "ladder", "IS_pick", "F_CAGR", "F_Sharpe", "F_MaxDD",
                 "F_H1", "F_H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "turnover_yr",
                 "pass4b_oos"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    k4bo = W[W["pass4b_oos"] == 1]
    say(f"\n  --- {len(k4bo)} instances clearing 4b on the OOS WINDOW ---")
    if len(k4bo):
        say(k4bo[["panel", "signal", "cost", "ladder", "IS_pick", "OOS_CAGR", "OOS_Sharpe",
                  "OOS_MaxDD", "pass4b_full"]].to_string(index=False,
                                                         float_format=lambda x: f"{x:.4f}"))

    # ---- textual census of published "argmax" claims
    say("\n=== CENSUS of published 'the argmax is X' claims ===")
    DIALS = {"GROSS": r"\bgross\b|\bg\s*=|\bm\s*=|de-gross",
             "COUNT": r"\btop-?\d|\bn\s*=|position count|book size",
             "CADENCE": r"cadence|monthly|weekly|daily|rebalanc",
             "VOLCAP": r"vol20|vol cap|max_vol|eligib",
             "VOLPOW": r"scaler|sqrt\(vol|vol scal",
             "SLEEVE": r"sleeve|f\s*=\s*0\.",
             "OTHER": r""}
    rows = []
    for fn in ("CHANGELOG.md", "QUEUE.md", "LEADERBOARD.md"):
        txt = (ROOT / "research" / fn).read_text()
        for m in re.finditer(r"argmax", txt, flags=re.I):
            ctx = txt[max(0, m.start() - 260): m.end() + 260].lower()
            hits = [d for d, pat in DIALS.items() if pat and re.search(pat, ctx)]
            rows.append(dict(file=fn, dial=";".join(hits) if hits else "OTHER",
                             ctx=re.sub(r"\s+", " ", ctx)[:200]))
    C = pd.DataFrame(rows)
    C.to_csv(OUT / f"{STEM}.census.csv", index=False)
    say(f"  {len(C)} textual 'argmax' claims across CHANGELOG/QUEUE/LEADERBOARD")
    counts = {}
    for d in DIALS:
        counts[d] = int(C["dial"].str.contains(d, regex=False).sum()) if len(C) else 0
    say("  claims mentioning each dial in context (non-exclusive): " +
        ", ".join(f"{d}={counts[d]}" for d in DIALS))
    audited = [d for d in ("GROSS", "COUNT", "CADENCE", "VOLCAP", "VOLPOW")]
    n_aud = int(C["dial"].str.contains("|".join(audited)).sum()) if len(C) else 0
    say(f"  {n_aud} of {len(C)} claims concern a dial this run re-ran; measured oracle-endpoint "
        f"share on those dials: " +
        ", ".join(f"{d} {per[d]['oe']:.2f}" for d in audited))

    # ---- verdict
    say("\n=== VERDICT ===")
    for lad in LADDERS:
        p = per[lad]
        sig_end = p["oe"] >= 0.80 and abs(p["rho_mean"]) >= 0.9
        say(f"  {lad:9s} oracle@end {p['oe']:.2f} (null {p['null']:.2f})  "
            f"rho(rank,meanOOS) {p['rho_mean']:+.2f}  cap_IS {p['capIS']:+.2f} "
            f"cap_RND {p['capRND']:+.2f}  -> "
            f"{'ENDPOINT ARTEFACT' if sig_end else 'not the 171 signature'}")

    pd.DataFrame(per).T.to_csv(OUT / f"{STEM}.summary.csv")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_console) + "\n")
    say(f"\ndone in {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_console) + "\n")


if __name__ == "__main__":
    main()
